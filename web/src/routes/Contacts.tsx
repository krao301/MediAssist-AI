import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getContacts, createContact, deleteContact } from '../lib/api';

interface Contact {
  id: number;
  name: string;
  phone: string;
  lat: number;
  lng: number;
  radius_m: number;
}

export default function Contacts() {
  const navigate = useNavigate();
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  
  // Form state
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');

  useEffect(() => {
    loadContacts();
  }, []);

  const loadContacts = async () => {
    try {
      const response = await getContacts();
      setContacts(response.data);
    } catch (error) {
      console.error('Failed to load contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddContact = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // For demo, use default coordinates
    // In production, geocode the address
    const lat = 42.9634; // Buffalo, NY
    const lng = -78.7384;
    
    try {
      await createContact(name, phone, lat, lng, 500);
      setName('');
      setPhone('');
      setAddress('');
      setShowAdd(false);
      loadContacts();
    } catch (error) {
      console.error('Failed to add contact:', error);
      alert('Failed to add contact');
    }
  };

  const handleDeleteContact = async (id: number) => {
    if (!confirm('Remove this contact?')) return;
    
    try {
      await deleteContact(id);
      loadContacts();
    } catch (error) {
      console.error('Failed to delete contact:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white">Loading contacts...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 sticky top-0 z-10 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/')}
              className="mr-4 text-2xl hover:opacity-75"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Trusted Contacts</h1>
          </div>
          <button
            onClick={() => setShowAdd(!showAdd)}
            className="bg-white text-blue-600 px-4 py-2 rounded-lg font-bold hover:bg-gray-100 transition"
          >
            {showAdd ? 'Cancel' : '+ Add Contact'}
          </button>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Info */}
        <div className="bg-blue-900/30 border border-blue-600 rounded-lg p-4 text-blue-200">
          <p className="text-sm">
            👥 Contacts within 500m will receive instant alerts during emergencies.
            Make sure to get their consent before adding them.
          </p>
        </div>

        {/* Add Contact Form */}
        {showAdd && (
          <form onSubmit={handleAddContact} className="bg-gray-800 rounded-lg p-6 space-y-4">
            <h3 className="text-white font-bold text-lg mb-4">Add New Contact</h3>
            
            <div>
              <label className="block text-gray-300 mb-2">Name *</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:border-blue-500 focus:outline-none"
                placeholder="John Doe"
              />
            </div>
            
            <div>
              <label className="block text-gray-300 mb-2">Phone Number *</label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:border-blue-500 focus:outline-none"
                placeholder="+1 (555) 123-4567"
              />
            </div>
            
            <div>
              <label className="block text-gray-300 mb-2">Home Address</label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:border-blue-500 focus:outline-none"
                placeholder="123 Main St, Buffalo, NY"
              />
              <p className="text-xs text-gray-500 mt-1">Used to calculate proximity to emergencies</p>
            </div>
            
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition"
            >
              Add Contact
            </button>
          </form>
        )}

        {/* Contacts List */}
        {contacts.length === 0 ? (
          <div className="bg-gray-800 rounded-lg p-12 text-center">
            <div className="text-6xl mb-4">👥</div>
            <h3 className="text-white text-xl font-bold mb-2">No contacts yet</h3>
            <p className="text-gray-400 mb-6">Add trusted people who can help in emergencies</p>
            <button
              onClick={() => setShowAdd(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-bold transition"
            >
              Add Your First Contact
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {contacts.map((contact) => (
              <div
                key={contact.id}
                className="bg-gray-800 rounded-lg p-4 flex items-center justify-between hover:bg-gray-750 transition"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-lg">
                    {contact.name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h4 className="text-white font-semibold">{contact.name}</h4>
                    <p className="text-gray-400 text-sm">{contact.phone}</p>
                    <p className="text-gray-500 text-xs mt-1">
                      📍 Alert radius: {contact.radius_m}m
                    </p>
                  </div>
                </div>
                
                <button
                  onClick={() => handleDeleteContact(contact.id)}
                  className="text-red-400 hover:text-red-300 font-bold px-4 py-2 rounded-lg hover:bg-red-900/30 transition"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
