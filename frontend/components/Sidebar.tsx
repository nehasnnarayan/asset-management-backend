"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import {
  Package,
  Users,
  LayoutDashboard,
  LogOut,
  Moon,
  Sun,
  ShieldAlert,
  Archive,
  User as UserIcon,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

// Types simulating a logged in user from mock state or JWT context
export type UserRole = "Admin" | "Employee" | null;

interface SidebarProps extends React.HTMLAttributes<HTMLDivElement> {
  userRole: UserRole;
  userName?: string;
}

export function Sidebar({ className, userRole, userName = "User", ...props }: SidebarProps) {
  const pathname = usePathname();
  const { setTheme, theme } = useTheme();

  return (
    <div className={cn("pb-12 border-r bg-sidebar h-screen flex flex-col", className)} {...props}>
      <div className="space-y-4 py-4 flex-1">
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight text-sidebar-foreground flex items-center gap-2">
            <Archive className="h-6 w-6 text-primary" />
            AssetTrack Pro
          </h2>
          <div className="space-y-1 mt-6">
            {/* FRONTEND RBAC: Admin vs Employee Links */}
            {userRole === "Admin" ? (
              <>
                <Button
                  variant={pathname === "/dashboard" ? "secondary" : "ghost"}
                  className="w-full justify-start"
                  asChild
                >
                  <Link href="/dashboard">
                    <LayoutDashboard className="mr-2 h-4 w-4" />
                    Dashboard
                  </Link>
                </Button>

                <div className="my-4 border-t px-4 py-2">
                  <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
                    <ShieldAlert className="h-3 w-3" />
                    Vault Management
                  </span>
                </div>
                
                <Button
                  variant={pathname === "/assets" ? "secondary" : "ghost"}
                  className="w-full justify-start text-primary"
                  asChild
                >
                  <Link href="/assets">
                    <Archive className="mr-2 h-4 w-4" />
                    All Assets
                  </Link>
                </Button>
                
                <Button
                  variant={pathname === "/employees" ? "secondary" : "ghost"}
                  className="w-full justify-start text-primary"
                  asChild
                >
                  <Link href="/employees">
                    <Users className="mr-2 h-4 w-4" />
                    Employees
                  </Link>
                </Button>
              </>
            ) : (
              <>
                <Button
                  variant={pathname === "/my-assets" ? "secondary" : "ghost"}
                  className="w-full justify-start"
                  asChild
                >
                  <Link href="/my-assets">
                    <Package className="mr-2 h-4 w-4" />
                    My Assets
                  </Link>
                </Button>

                <Button
                  variant={pathname === "/profile" ? "secondary" : "ghost"}
                  className="w-full justify-start"
                  asChild
                >
                  <Link href="/profile">
                    <UserIcon className="mr-2 h-4 w-4" />
                    Profile
                  </Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
      
      {/* Footer / User Area */}
      <div className="mt-auto border-t p-4 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="bg-primary/10 text-primary text-xs">
                {userName.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="text-sm font-medium">{userName}</span>
              <span className="text-xs text-muted-foreground">{userRole}</span>
            </div>
          </div>
          
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="h-8 w-8"
          >
            <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
        
        <Button variant="outline" className="w-full justify-start text-muted-foreground">
          <LogOut className="mr-2 h-4 w-4" />
          Log out
        </Button>
      </div>
    </div>
  );
}
