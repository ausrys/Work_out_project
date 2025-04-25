import { useState } from "react";
import api from "../../api/axios";

type Props = {}

function ProgramForm({}: Props) {
    const [formData, setFormData] = useState({
        name: '',
        level: '',
        program_description: '',
        date: '',
      });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData({
          ...formData,
          [name]: value,
        });
      };
      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
    
        try {
          const response = await api.post('/programs/create', formData)
          setMessage(response.data.message);
          setError('');
        } catch (err: any) {
          setError(err.response?.data?.error || 'Something went wrong');
          setMessage('');
        }
      };
  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded-md shadow-md">
    <h2 className="text-xl font-semibold text-center mb-4">Program Registration</h2>

    <form onSubmit={handleSubmit}>
      <div className="mb-4">
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Program Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="level" className="block text-sm font-medium text-gray-700">Level ID</label>
        <input
          type="number"
          id="level"
          name="level"
          value={formData.level}
          onChange={handleChange}
          required
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="program_description" className="block text-sm font-medium text-gray-700">Program Description</label>
        <textarea
          id="program_description"
          name="program_description"
          value={formData.program_description}
          onChange={handleChange}
          required
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="date" className="block text-sm font-medium text-gray-700">Program Date</label>
        <input
          type="date"
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
      >
        Register Program
      </button>
    </form>

    {message && <div className="mt-4 text-green-500">{message}</div>}
    {error && <div className="mt-4 text-red-500">{error}</div>}
  </div>
  )
}

export default ProgramForm