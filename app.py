import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List
from models import Contact  
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["contacts_db"]
collection = db["contacts"]

# FastAPI app setup
app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/contacts/", response_model=Contact)
def create_contact(contact: Contact):
    contact_dict = contact.dict(exclude_unset=True)
    result = collection.insert_one(contact_dict)
    
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to create contact")
    
    contact.id = str(result.inserted_id)
    logger.info(f"Created contact: {contact}")
    return contact

@app.get("/contacts/", response_model=List[Contact])
def get_contacts():
    contacts = []
    try:
        for contact in collection.find():
            contact["id"] = str(contact["_id"])
            contacts.append(contact)
        logger.info(f"Fetched contacts: {contacts}")
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching contacts")
    
    return contacts

@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: str):
    try:
        contact = collection.find_one({"_id": ObjectId(contact_id)})
        if contact:
            contact["id"] = str(contact["_id"])
            logger.info(f"Fetched contact: {contact}")
            return contact
        else:
            raise HTTPException(status_code=404, detail="Contact not found")
    except Exception as e:
        logger.error(f"Error fetching contact with ID {contact_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching contact")

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: str, contact: Contact):
    contact_dict = contact.dict(exclude_unset=True)
    try:
        result = collection.update_one({"_id": ObjectId(contact_id)}, {"$set": contact_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        contact.id = contact_id
        logger.info(f"Updated contact: {contact}")
        return contact
    except Exception as e:
        logger.error(f"Error updating contact with ID {contact_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating contact")

@app.delete("/contacts/{contact_id}", response_model=dict)
def delete_contact(contact_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(contact_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        logger.info(f"Deleted contact with ID: {contact_id}")
        return {"message": f"Contact with ID {contact_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting contact with ID {contact_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting contact")
