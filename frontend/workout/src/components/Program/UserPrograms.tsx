import { useEffect, useState } from "react";
interface CustomExercise {
  id: number;
  reps: number;
  sets: number;
  weight: number;
  base_exercise_name: string;
}
interface UserProgram {
  id: number;
  name: string;
  description: string;
  is_custom: boolean;
  created_at: string;
  exercises: CustomExercise[];
}
function UserPrograms() {
  const [programs, setPrograms] = useState<UserProgram[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found");
      return;
    }

    fetch("http://127.0.0.1:8000/user/programs/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch programs");
        }
        return res.json();
      })
      .then((data: UserProgram[]) => {
        setPrograms(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching programs:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;

  if (!programs || programs.length === 0) return <p>No programs found.</p>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Your Programs</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {programs.map((program) => (
          <div key={program.id} className="p-4 shadow rounded border">
            <h3 className="text-lg font-semibold">{program.name}</h3>
            <p className="text-sm text-gray-600 mb-2">{program.description}</p>
            <ul className="text-sm list-disc pl-5">
              {program.exercises?.map((exercise) => (
                <li key={exercise.id}>
                  {exercise.base_exercise_name} – {exercise.reps} reps ×{" "}
                  {exercise.sets} sets
                  {exercise.weight > 0 && ` – ${exercise.weight} kg`}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
export default UserPrograms;
