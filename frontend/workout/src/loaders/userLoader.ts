import { redirect } from "react-router";
import { queryClient } from "../queryClient";
import { getUserProfile } from "../api/apiFns";
export const userLoader = async () => {
  try {
    return await queryClient.fetchQuery({
      queryKey: ["userProfile"],
      queryFn: getUserProfile
    });
  } catch (err: any) {
    if (err.response?.status === 401) {
      return redirect("/login");
    }
    throw err;
  }
};