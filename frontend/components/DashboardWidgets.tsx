import { Activity, CreditCard, DollarSign, Users } from "lucide-react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export function StatCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">1,245</div>
          <p className="text-xs text-muted-foreground">+20 from last month</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Assigned Assets</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">890</div>
          <p className="text-xs text-muted-foreground">+54 assigned this week</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Available Assets</CardTitle>
          <CreditCard className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">230</div>
          <p className="text-xs text-muted-foreground">-12 from last week</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Maintenance</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">125</div>
          <p className="text-xs text-muted-foreground">+2 currently repairing</p>
        </CardContent>
      </Card>
    </div>
  );
}

const recentAssignments = [
  { id: "A-1029", asset: "MacBook Pro 16", employee: "John Doe", date: "2026-03-05", status: "Active" },
  { id: "A-1030", asset: "Dell UltraSharp 27", employee: "Jane Smith", date: "2026-03-04", status: "Active" },
  { id: "A-1031", asset: "ErgoChair Pro", employee: "Alice Webb", date: "2026-03-04", status: "Pending" },
  { id: "A-1032", asset: "Lenovo ThinkPad X1", employee: "Bob Martin", date: "2026-03-02", status: "Active" },
  { id: "A-1033", asset: "Apple Magic Keyboard", employee: "Charlie Day", date: "2026-03-01", status: "Returned" },
];

export function RecentActivityTable() {
  return (
    <Card className="col-span-3">
      <CardHeader>
        <CardTitle>Recent Assignments</CardTitle>
        <CardDescription>
          Tracking the latest 5 asset provisions across the organization.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">Asset ID</TableHead>
              <TableHead>Asset Name</TableHead>
              <TableHead>Employee</TableHead>
              <TableHead className="text-right">Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {recentAssignments.map((assignment) => (
              <TableRow key={assignment.id}>
                <TableCell className="font-medium">{assignment.id}</TableCell>
                <TableCell>{assignment.asset}</TableCell>
                <TableCell>{assignment.employee}</TableCell>
                <TableCell className="text-right">
                  <Badge variant={assignment.status === "Active" ? "default" : assignment.status === "Returned" ? "outline" : "secondary"}>
                    {assignment.status}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
