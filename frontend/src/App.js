import React, { useState } from 'react';
import axios from 'axios';
import ContactForm from './components/ContactForm';
import ContactList from './components/ContactList';

const App = () => {
    const [contacts, setContacts] = useState([]);

    const fetchContacts = async () => {
        try {
            const response = await axios.get('http://localhost:8000/contacts/');
            setContacts(response.data);
        } catch (error) {
            console.error("Error fetching contacts:", error);
        }
    };

    return (
        <div>
            <h1>Contact Management</h1>
            <ContactForm fetchContacts={fetchContacts} />
            <ContactList contacts={contacts} fetchContacts={fetchContacts} />
        </div>
    );
};

export default App;
