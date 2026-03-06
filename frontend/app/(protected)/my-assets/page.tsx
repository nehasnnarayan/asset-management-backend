import { AlertTriangle, Laptop } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function MyAssetsPage() {
  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">My Assigned Gear</h1>
        <p className="text-muted-foreground mt-2">
          Review the equipment issued to you. Report any issues or request maintenance.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mt-8">
        {/* Placeholder assigned mock asset */}
        <Card className="flex flex-col">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <CardTitle>ThinkPad T14 Gen 3</CardTitle>
                <CardDescription className="mt-1">ID: A-4902-LT</CardDescription>
              </div>
              <Laptop className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent className="flex-1">
            <div className="space-y-2 text-sm text-muted-foreground">
              <p>Type: Laptop</p>
              <p>Assigned On: Mar 1, 2026</p>
              <div className="flex mt-2">
                 <Badge variant="outline" className="text-green-500 border-green-200 bg-green-50 dark:bg-green-950/20">Excellent Condition</Badge>
              </div>
            </div>
          </CardContent>
          <CardFooter className="border-t bg-muted/30 pt-4 mt-auto">
            <Button variant="outline" className="w-full text-amber-600 border-amber-200 hover:bg-amber-50 dark:hover:bg-amber-900/20">
              <AlertTriangle className="mr-2 h-4 w-4" />
              Report Issue
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
