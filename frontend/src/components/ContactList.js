import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ContactList = ({ fetchContacts }) => {
    const [contacts, setContacts] = useState([]);

    const fetchData = async () => {
        const response = await axios.get('http://localhost:8000/contacts/');
        setContacts(response.data);
    };

    const handleDelete = async (id) => {
        await axios.delete(`http://localhost:8000/contacts/${id}`);
        fetchContacts();
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            {contacts.map(contact => (
                <div key={contact.id}>
                    <h3>{contact.name}</h3>
                    <p>{contact.email}</p>
                    <p>{contact.phone}</p>
                    <button onClick={() => handleDelete(contact.id)}>Delete</button>
                </div>
            ))}
        </div>
    );
};

export default ContactList;
