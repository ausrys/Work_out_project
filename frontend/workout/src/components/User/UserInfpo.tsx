import { useEffect, useState } from "react";
import { Link } from "react-router";
import api from "../../api/axios";

interface Sportsman {
  id: number;
  name: string;
  email: string;
  age: number;
  weight: number;
  gender: string;
  subscription_level: string;
  city: number | null;
  level: number | null;
}
function UserInfpo() {
  const [user, setUser] = useState<Sportsman | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await api.get("user-info/")
        if (!response) {
          throw new Error("Failed to fetch user profile.");
        }
        setUser(response.data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);
  if (loading) return <p>Loading profile...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!user) return <p>No user data available.</p>;
  return (
    <div className="p-4 border rounded shadow-md max-w-md mx-auto mt-6">
      <h2 className="text-2xl font-bold mb-4">User Profile</h2>
      <p>
        <strong>Name:</strong> {user.name}
      </p>
      <p>
        <strong>Email:</strong> {user.email}
      </p>
      <p>
        <strong>Age:</strong> {user.age}
      </p>
      <p>
        <strong>Weight:</strong> {user.weight} kg
      </p>
      <p>
        <strong>Gender:</strong> {user.gender}
      </p>
      <p>
        <strong>Subscription:</strong> {user.subscription_level}{" "}
        <Link
          to="/change-subscription"
          className="text-blue-600 underline hover:text-blue-800 ml-2"
        >
          Change
        </Link>
      </p>
      <p>
        <strong>City ID:</strong> {user.city ?? "N/A"}
      </p>
      <p>
        <strong>Level ID:</strong> {user.level ?? "N/A"}
      </p>
    </div>
  );
}
export default UserInfpo;
