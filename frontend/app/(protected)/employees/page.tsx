import { UserPlus, Users } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/SharedUtility";

export default function EmployeesPage() {
  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Employee Directory</h1>
          <p className="text-muted-foreground mt-2">
            View all staff members and manage their assigned hardware.
          </p>
        </div>
        
        <Button>
          <UserPlus className="mr-2 h-4 w-4" />
          Onboard Employee
        </Button>
      </div>

      <div className="mt-8 border rounded-lg bg-card p-4 shadow-sm">
        <EmptyState 
          title="No Employees Found" 
          icon={<Users className="h-12 w-12 text-muted-foreground/50" />}
          description="The employee directory is currently empty. Onboard staff to assign assets."
        />
      </div>
    </div>
  );
}
