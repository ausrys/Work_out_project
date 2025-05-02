import { useEffect, useState } from "react";
import { Coach } from "../types/types";
import CoachCard from "./Coach";

type Props = {};
function Coaches({}: Props) {
  const [coaches, setCoaches] = useState<Coach[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch("http://localhost:8000/coaches/")
      .then((res) => res.json())
      .then((data) => {
        setCoaches(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching coaches:", error);
        setLoading(false);
      });
  }, []);
  if (loading) return <p>Loading coaches...</p>;
  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Our Coaches</h2>
      <ul className="space-y-2">
        {coaches.map((coach) => (
          <CoachCard key={coach.id} coach={coach} />
        ))}
      </ul>
    </div>
  );
}
export default Coaches;
