/**
 * API client for Launch Go/No-Go Advisor backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface LaunchSite {
  code: string;
  name: string;
  lat: number;
  lon: number;
}

export interface LaunchRequest {
  site_code: string;
  launch_time: string;
}

export interface LaunchResponse {
  verdict: 'GO' | 'NO-GO' | 'MARGINAL' | 'ERROR';
  risk_score: number;
  why: string;
  rule_citations: string[];
  data?: {
    weather?: any;
    space_weather?: any;
    conjunction?: any;
  };
}

export async function getSites(): Promise<LaunchSite[]> {
  const response = await fetch(`${API_BASE_URL}/sites`);
  if (!response.ok) {
    throw new Error('Failed to fetch launch sites');
  }
  const data = await response.json();
  return data.sites;
}

export async function decideLaunch(request: LaunchRequest): Promise<LaunchResponse> {
  const response = await fetch(`${API_BASE_URL}/api/decide`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get launch decision');
  }

  return response.json();
}
