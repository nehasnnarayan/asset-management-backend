import { StatCards, RecentActivityTable } from "@/components/DashboardWidgets";

export default function DashboardPage() {
  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500 relative z-10">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard Overview</h1>
        <p className="text-muted-foreground mt-2">
          Welcome to the AssetTrack Pro vault. Choose an option from the sidebar to manage inventory.
        </p>
      </div>
      
      <StatCards />
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-4">
        <div className="col-span-4 lg:col-span-7">
           <RecentActivityTable />
        </div>
      </div>
    </div>
  );
}
