import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getContacts, createContact, deleteContact } from '../lib/api';

export default function Contacts() {
  const navigate = useNavigate();
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);

  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');

  useEffect(() => {
    loadContacts();
  }, []);

  const loadContacts = async () => {
    try {
      const response = await getContacts();
      setContacts(response.data || []);
    } catch (error) {
      console.error('Failed to load contacts', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddContact = async (e) => {
    e.preventDefault();
    if (!name || !phone || !address) return;

    try {
      // NOTE: For simplicity we don't geocode here; you can hook up real geocoding if needed.
      const lat = 0;
      const lng = 0;
      const radiusM = 500;

      await createContact(name, phone, lat, lng, radiusM);
      setName('');
      setPhone('');
      setAddress('');
      setShowAdd(false);
      await loadContacts();
    } catch (error) {
      console.error('Failed to create contact', error);
    }
  };

  const handleDeleteContact = async (id) => {
    try {
      await deleteContact(id);
      setContacts(prev => prev.filter(c => c.id !== id));
    } catch (error) {
      console.error('Failed to delete contact', error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-3xl mx-auto px-4 py-5">
        <div className="flex items-center justify-between gap-3 mb-4">
          <div>
            <h1 className="text-lg font-semibold text-sky-400">
              Emergency Contacts
            </h1>
            <p className="text-[11px] text-slate-400">
              Save trusted people who should be notified during emergencies.
            </p>
          </div>
          <button
            onClick={() => navigate('/')}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-200"
          >
            ← Back to Home
          </button>
        </div>

        <div className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-3 mb-4">
          <div className="flex items-start gap-2">
            <div className="w-7 h-7 rounded-full bg-sky-500/15 border border-sky-400/40 flex items-center justify-center text-sky-300 text-xs font-semibold">
              ☎
            </div>
            <div className="flex-1">
              <p className="text-[10px] text-slate-300 mb-1">
                When enabled, MediAssist AI can use these contacts for automated SMS or call workflows
                triggered by critical incidents.
              </p>
            </div>
          </div>
        </div>

        <div className="mb-4">
          <button
            onClick={() => setShowAdd(prev => !prev)}
            className="px-3 py-2 rounded-lg bg-sky-500 hover:bg-sky-600 text-slate-950 text-[10px] font-semibold"
          >
            {showAdd ? 'Cancel' : '➕ Add New Contact'}
          </button>
        </div>

        {showAdd && (
          <form
            onSubmit={handleAddContact}
            className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-3 mb-4 grid gap-2 text-[10px]"
          >
            <div className="grid gap-1">
              <label className="text-slate-400">Name</label>
              <input
                value={name}
                onChange={e => setName(e.target.value)}
                className="px-2 py-1.5 rounded-lg bg-slate-950/80 border border-slate-700/80 text-slate-100 text-[10px] outline-none focus:ring-1 focus:ring-sky-500"
                placeholder="Contact name"
              />
            </div>
            <div className="grid gap-1">
              <label className="text-slate-400">Phone</label>
              <input
                value={phone}
                onChange={e => setPhone(e.target.value)}
                className="px-2 py-1.5 rounded-lg bg-slate-950/80 border border-slate-700/80 text-slate-100 text-[10px] outline-none focus:ring-1 focus:ring-sky-500"
                placeholder="E.164 format recommended"
              />
            </div>
            <div className="grid gap-1">
              <label className="text-slate-400">Location / Notes</label>
              <input
                value={address}
                onChange={e => setAddress(e.target.value)}
                className="px-2 py-1.5 rounded-lg bg-slate-950/80 border border-slate-700/80 text-slate-100 text-[10px] outline-none focus:ring-1 focus:ring-sky-500"
                placeholder="Location or additional info"
              />
            </div>

            <div className="flex justify-end gap-2 mt-2">
              <button
                type="button"
                onClick={() => setShowAdd(false)}
                className="px-3 py-1.5 rounded-lg border border-slate-700/80 text-slate-300 text-[10px]"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-slate-950 text-[10px] font-semibold"
              >
                Save Contact
              </button>
            </div>
          </form>
        )}

        {loading ? (
          <div className="text-[11px] text-slate-400">
            Loading contacts...
          </div>
        ) : contacts.length === 0 ? (
          <div className="text-[11px] text-slate-500">
            No contacts saved yet. Add someone you trust so they can be notified.
          </div>
        ) : (
          <div className="grid gap-2">
            {contacts.map((contact) => (
              <div
                key={contact.id}
                className="bg-slate-900/80 border border-slate-800/80 rounded-2xl p-3 flex items-center justify-between gap-3 text-[10px]"
              >
                <div>
                  <p className="font-semibold text-slate-100">
                    {contact.name}
                  </p>
                  <p className="text-sky-300 text-[10px]">
                    {contact.phone}
                  </p>
                  <p className="text-slate-500 text-[9px] mt-1">
                    Radius: {contact.radius_m || 500}m
                  </p>
                </div>
                <button
                  onClick={() => handleDeleteContact(contact.id)}
                  className="text-red-400 hover:text-red-300 font-bold px-3 py-1.5 rounded-lg hover:bg-red-900/30 transition"
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
