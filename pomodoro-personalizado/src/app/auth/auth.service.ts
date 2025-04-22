import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api/auth';
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient, private router: Router) {
    // Verifica se há token armazenado ao inicializar
    this.checkToken();
  }

  // Método para fazer login
  login(credentials: { email: string; password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
      tap((response: any) => {
        // Armazena o token no localStorage
        localStorage.setItem('authToken', response.token);
        this.isAuthenticatedSubject.next(true);
      })
    );
  }

  // Método para fazer logout
  logout(): void {
    localStorage.removeItem('authToken');
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/login']);
  }

  // Verifica se o usuário está autenticado
  isAuthenticated(): Observable<boolean> {
    return this.isAuthenticatedSubject.asObservable();
  }

  // Obtém o token
  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  // Verifica se há token válido
  private checkToken(): void {
    const token = this.getToken();
    this.isAuthenticatedSubject.next(!!token);
  }
}