import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { AuthGuard } from './auth/auth.guard';

export const routes: Routes = [
  { 
    path: 'login', 
    component: LoginComponent,
    title: 'Login' 
  },
  { 
    path: '', 
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent),
    title: 'Dashboard',
    canActivate: [AuthGuard]
  },
  { 
    path: '**', 
    redirectTo: '/login',
    pathMatch: 'full' 
  }
];