import { Sidebar } from "@/components/Sidebar";
import { TopNavbar } from "@/components/TopNavbar";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Hardcoded 'Admin' for Screenshot A, 'Employee' for Screenshot B.
  const role = "Admin";
  const userName = role === "Admin" ? "Boss Admin" : "Standard Employee";

  return (
    <div className="flex h-screen overflow-hidden crypto-bg">
      <Sidebar userRole={role} userName={userName} className="w-64 flex-shrink-0 hidden md:flex z-10" />

      <div className="flex-1 flex flex-col overflow-hidden z-10">
        <TopNavbar role={role} userName={userName} />

        <main className="flex-1 overflow-auto bg-muted/20 p-4 md:p-6 lg:p-8 relative">
          {children}
        </main>
      </div>
    </div>
  );
}
