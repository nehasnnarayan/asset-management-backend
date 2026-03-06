import { PackagePlus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/SharedUtility";

export default function AssetsPage() {
  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Asset Inventory</h1>
          <p className="text-muted-foreground mt-2">
            Manage all company assets. Add new hardware, edit details, or decommission items.
          </p>
        </div>
        
        <Button>
          <PackagePlus className="mr-2 h-4 w-4" />
          Add New Asset
        </Button>
      </div>

      <div className="mt-8 border rounded-lg bg-card p-4 shadow-sm">
        <EmptyState 
          title="No Assets Found" 
          description="You haven't added any assets to the database yet. Click the button above to start provisioning hardware."
          action={
            <Button variant="outline" className="mt-4">
              <PackagePlus className="mr-2 h-4 w-4" />
              Add First Asset
            </Button>
          }
        />
      </div>
    </div>
  );
}
