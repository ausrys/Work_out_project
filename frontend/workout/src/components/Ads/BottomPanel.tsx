import { useQuery } from "@tanstack/react-query";
import api from "../../api/axios";

function BottomPanel() {
  const { data: ads, isLoading, error } = useQuery({
    queryKey: ["ads"],
    queryFn: async () => {
      const res = await api.get("get-advertiser-data/");
      return res.data;
    },
    staleTime: 10 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    retry: false
  });

  if (isLoading || error || !ads?.length) return null;

  const lowPriorityAds = ads.filter((ad: any) => ad.priority === 0);

  if (lowPriorityAds.length === 0) return null;
  
  return (
    <section className="w-full p-4 bg-white border-t border-gray-300 flex flex-wrap gap-4">
      {lowPriorityAds.map((ad: any, index: number) => (
        <div key={index} className="p-3 border rounded shadow-sm max-w-xs text-left">
          {Object.entries(ad.data).map(([key, value]) => (
            <div key={key} className="text-sm break-words">
              <strong>{key}: </strong> {String(value)}
            </div>
          ))}
        </div>
      ))}
    </section>
  );
}

export default BottomPanel;
