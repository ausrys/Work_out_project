import { loadStripe } from "@stripe/stripe-js";
import api from "../../api/axios";
const public_key = import.meta.env.VITE_STRIPE_PUBLIC_KEY
const stripePromise = loadStripe(public_key);
type Props = {}

function Stripe({}: Props) {
    const handleCheckout = async () => {
        const { data } = await api.post("/create-checkout-session/");
        const stripe = await stripePromise;
        await stripe?.redirectToCheckout({ sessionId: data.id });
      };
  return (
    <div><button onClick={handleCheckout}>Upgrade to Premium</button></div>
  )
}

export default Stripe