import { useEffect, useState } from "react";
import api from "../../api/axios";

interface UserPayment {
    id: number;
    payment_value: number;
    date_time: string;
  }

function PaymentsList() {
    const [payments, setPayments] = useState<UserPayment[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/payments/")
          .then((res) => {
            setPayments(res.data);
            setLoading(false);
          })
          .catch((err) => {
            console.error("Failed to fetch payments", err);
            setLoading(false);
          });
      }, []);
      if (loading) return <div>Loading payments...</div>;
      return (
        <div>
          <h2>Your Payment History</h2>
          {payments.length === 0 ? (
            <p>No payments found.</p>
          ) : (
            <ul>
              {payments.map((payment) => (
                <li key={payment.id}>
                ${payment.payment_value} —{" "}
                  {new Date(payment.date_time).toLocaleString()}
                </li>
              ))}
            </ul>
          )}
        </div>
      );
}

export default PaymentsList