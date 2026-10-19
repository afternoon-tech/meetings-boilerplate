import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { http } from './http';

export type CalendarProvider = 'GOOGLE' | 'MICROSOFT';

export interface Advisor {
  id: string;
  name: string;
  email: string;
}

export interface CalendarConnection {
  id: string;
  provider: CalendarProvider;
  accountEmail: string;
  advisor: Advisor;
  lastSyncedAt: string | null;
}

export interface Client {
  id: string;
  name: string;
  email: string;
}

export interface Meeting {
  id: string;
  title: string;
  startsAt: string;
  endsAt: string;
}

export const queryKeys = {
  meetings: ['meetings'] as const,
  calendarConnections: ['calendar-connections'] as const,
  clients: ['clients'] as const,
};

export function useMeetings() {
  return useQuery({ queryKey: queryKeys.meetings, queryFn: () => http<Meeting[]>('/api/meetings') });
}

export function useCalendarConnections() {
  return useQuery({
    queryKey: queryKeys.calendarConnections,
    queryFn: () => http<CalendarConnection[]>('/api/calendar-connections'),
  });
}

export function useClients() {
  return useQuery({ queryKey: queryKeys.clients, queryFn: () => http<Client[]>('/api/clients') });
}

export function useSyncMeetings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => http<void>('/api/meetings/sync', { method: 'POST' }),
    onSettled: () => {
      void queryClient.invalidateQueries({ queryKey: queryKeys.meetings });
      void queryClient.invalidateQueries({ queryKey: queryKeys.calendarConnections });
    },
  });
}
