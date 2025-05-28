import api from "../../api/axios";
import { useQuery } from "@tanstack/react-query";

function RightPanel() {
    const {data: ads, isLoading, error} = useQuery({
        queryKey: ["ads"],
        queryFn: async () => {
            const res =await api.get("get-advertiser-data/");
            return res.data;
        },
        staleTime: 10  * 60 *1000,
        gcTime: 10 * 60 * 1000,
        retry: false
    })
    
    if (isLoading || error || !ads?.length) return null;
    const midPrioAdds = ads.filter((ad: any) => ad.priority === 1);
    return (
        <aside className="w-64 min-h-screen p-4 border-l border-gray-300 bg-white overflow-y-auto">
          <h2 className="font-bold text-lg mb-2">Sponsored Ads</h2>
          {midPrioAdds.map((ad: any, index: number) => (
            <div key={index} className="mb-4 p-2 border rounded shadow-sm">
                <h3 className="font-semibold">{ad.company}</h3>
                <p>{ad.description}</p>
              {Object.entries(ad.data).map(([key, value]) => (
                <div key={key} className="text-sm break-words">
                  {String(value)}
                </div>
              ))}
            </div>
          ))}
        </aside>
      );
}

export default RightPanel