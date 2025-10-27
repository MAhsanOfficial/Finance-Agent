# from agents import Agent , Runner , OpenAIChatCompletionsModel,AsyncOpenAI,  set_tracing_disabled,function_tool
# import requests
# import os
# from mockdata import mockdata
# from dotenv import load_dotenv
# load_dotenv()
# from fastapi import FastAPI
# set_tracing_disabled(True)



# app = FastAPI()


# gemini_api_key  = os.getenv("GEMINI_API_KEY")


# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )       
# model = OpenAIChatCompletionsModel(
#     model  = "gemini-2.0-flash",
#     openai_client=external_client,
# )


# @function_tool
# def payment_detail():
#     """
#     The tool is to fetch the payment details from the database
#     """
#     data = mockdata
#     return data



# @function_tool
# def passing_data():
#     """
    
#     """
#     if mockdata[0].status == 'Sucess':
#         print('fastapi ==>>  database / mcp')
#     return post_data()



# @app.get("/")
# def payment_details():
#     data = mockdata
#     return {"payment_details": data}

# @app.post("/postdata/")
# def post_data():
#     return {"message": "Data passed successfully"}





# agent  = Agent(
#     name  = "Finance Agent",
#     instructions="You Are Finance Expert",
#     model=model,
#     tools=[payment_detail]
# )
# if __name__ == "__main__":
#     # When run directly (python main.py) we execute the agent synchronously.
#     # Avoid running this at import time so uvicorn (which already runs an
#     # event loop) doesn't raise "This event loop is already running".
#     result = Runner.run_sync(
#         agent,
#         input="Hey",
#     )
#     print(result.final_output)










# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os, requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# local imports
from mockdata import mockdata
from database import SessionLocal, engine
from models import Payment
from sqlalchemy.exc import SQLAlchemyError

# Try to import agents, but handle gracefully if not available
try:
    from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool
    set_tracing_disabled(True)
    AGENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Agents module not available: {e}")
    AGENTS_AVAILABLE = False

# Create tables (if not exist)
try:
    Payment.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")

app = FastAPI(
    title="Finance Agent API",
    description="A FastAPI application for managing payment data with AI agent integration",
    version="1.0.0"
)

# Health check endpoint
@app.get("/health")
def health_check():
    from database import DATABASE_URL
    return {
        "status": "healthy",
        "agents_available": AGENTS_AVAILABLE,
        "agent_initialized": agent is not None if 'agent' in globals() else False,
        "database_url": DATABASE_URL
    }

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route: view mockdata (existing)
@app.get("/")
def payment_details():
    return {"payment_details": mockdata}

# Route: save mockdata to DB
@app.post("/save-to-db/")
def save_to_db(db: Session = Depends(get_db)):
    try:
        saved = []
        for data in mockdata:
            # If mockdata items are dicts, use data['order_id'] else attributes
            order_id = getattr(data, "order_id", None) or data.get("order_id")
            customer_name = getattr(data, "customer_name", None) or data.get("customer_name")
            amount = getattr(data, "amount", None) or data.get("amount")
            status = getattr(data, "status", None) or data.get("status")
            tx_id = getattr(data, "tx_id", None) or data.get("tx_id")

            payment = Payment(
                order_id=order_id,
                customer_name=customer_name,
                amount=amount,
                status=status,
                tx_id=tx_id
            )
            db.add(payment)
            saved.append(order_id)
        db.commit()
        return {"message": "Data saved to database successfully", "saved_orders": saved}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Route: return only SUCCESS payments saved to database
@app.get("/get-payments/")
def get_payments(db: Session = Depends(get_db)):
    # Only get payments with SUCCESS status
    items = db.query(Payment).filter(Payment.status == "SUCCESS").all()
    # convert to serializable dicts
    return [{"id": p.id, "order_id": p.order_id, "customer_name": p.customer_name,
             "amount": p.amount, "status": p.status, "tx_id": p.tx_id} for p in items]


# ----------------- Agent setup -----------------
agent = None
if AGENTS_AVAILABLE:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        logger.warning("GEMINI_API_KEY not found in environment variables. Agent will not be available.")
    else:
        try:
            external_client = AsyncOpenAI(
                api_key=gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            model = OpenAIChatCompletionsModel(
                model="gemini-2.0-flash",
                openai_client=external_client,
            )

            # Tool the agent can call to instruct FastAPI to save
            @function_tool
            def save_payment_data_via_api():
                """
                Agent tool: calls internal FastAPI endpoint to save mockdata into DB.
                Ensure uvicorn is running before agent calls this.
                """
                try:
                    resp = requests.post("http://localhost:8000/save-to-db/", timeout=10)
                    return resp.json()
                except Exception as e:
                    return {"error": str(e)}

            # Tool the agent can call to get SUCCESS payments from database
            @function_tool
            def get_success_payments():
                """
                Agent tool: calls internal FastAPI endpoint to get only SUCCESS payment records from DB.
                """
                try:
                    resp = requests.get("http://localhost:8000/get-payments/", timeout=10)
                    return resp.json()
                except Exception as e:
                    return {"error": str(e)}

            agent = Agent(
                name="Finance Agent",
                instructions=(
                    "You are Finance Agent. Use the 'save_payment_data_via_api' tool to save payment records "
                    "to the database, then use 'get_success_payments' to retrieve only SUCCESS status payments. "
                    "Respond concisely in JSON with fields: action, message, success_payments_count, success_payments."
                ),
                model=model,
                tools=[save_payment_data_via_api, get_success_payments]
            )
            logger.info("Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            agent = None

# Endpoint to demonstrate agent workflow (save data and get SUCCESS payments)
@app.get("/run-agent/")
def run_agent():
    if not agent:
        raise HTTPException(
            status_code=503, 
            detail="Agent not available. Please check GEMINI_API_KEY environment variable and agents module installation."
        )
    
    try:
        # Step 1: Save data to database
        save_response = requests.post("http://localhost:8000/save-to-db/", timeout=10)
        save_result = save_response.json()
        
        # Step 2: Get only SUCCESS payments
        get_response = requests.get("http://localhost:8000/get-payments/", timeout=10)
        success_payments = get_response.json()
        
        return {
            "action": "agent_workflow_completed",
            "message": "Data saved and SUCCESS payments retrieved",
            "save_result": save_result,
            "success_payments_count": len(success_payments),
            "success_payments": success_payments
        }
            
    except Exception as e:
        logger.error(f"Agent workflow failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent workflow failed: {str(e)}")

# If you want to run directly (not via uvicorn), avoid starting uvicorn inside
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
