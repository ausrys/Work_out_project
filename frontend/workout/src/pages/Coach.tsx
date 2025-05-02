import { Coach } from "../types/types";

interface CoachCardProps {
  coach: Coach;
}

const CoachCard: React.FC<CoachCardProps> = ({ coach }) => {
  return (
    <div className="border p-3 rounded shadow">
      <p>
        <strong>Name:</strong> {coach.name}
      </p>
      <p>
        <strong>Email:</strong> {coach.email}
      </p>
      <p>
        <strong>Age:</strong> {coach.age}
      </p>
      <p>
        <strong>City:</strong> {coach.city}
      </p>
      <p>
        <strong>Experience:</strong> {coach.years_of_experience} years
      </p>
    </div>
  );
};

export default CoachCard;
