import React, { useState } from "react";
import api from "../../api/axios";
import { useNavigate } from "react-router";
import TextInput from "../Reusable/TextInput";
import SelectInput from "../Reusable/SelectInput";

interface FormData {
  name: string;
  password: string;
  age: number;
  city: string;
  level: number;
  email: string;
  weight: number;
  gender: "male" | "female" ;
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    password: "",
    age: 0,
    city: "",
    level: 1,
    email: "",
    weight: 0,
    gender: "male", // default value
  });
  const navigate = useNavigate();
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response  = await api.post("registration/", formData);
      console.log(response);
      navigate("/home");
    } catch (error: any) {
      if (error.response) {
        alert("Registration failed: " + JSON.stringify(error.response.data));
      } else {
        alert("Something went wrong: " + error.message);
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow-md w-full max-w-sm"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Register</h2>

        <TextInput label="Username" name="name" value={formData.name} onChange={handleChange} required />
        <TextInput label="Email" name="email" type="email" value={formData.email} onChange={handleChange} required />
        <TextInput label="Password" name="password" type="password" value={formData.password} onChange={handleChange} required />
        <TextInput label="Age" name="age" type="number" value={formData.age} onChange={handleChange} required />
        <TextInput label="City" name="city" value={formData.city} onChange={handleChange} required />
        <TextInput label="Level" name="level" type="number" value={formData.level} onChange={handleChange} required />
        <TextInput label="Weight" name="weight" type="number" value={formData.weight} onChange={handleChange} required />
        <SelectInput
              label="Gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              options={[
                { label: "Male", value: "male" },
                { label: "Female", value: "female" },
              ]}
              required
/>
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition"
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default RegisterForm;
