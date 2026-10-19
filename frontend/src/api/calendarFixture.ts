import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { http } from './http';

const calendarFixtureKey = ['dev', 'calendar-fixture'] as const;

/** The stubbed providers' remote state. Shape mirrors `CalendarFixture` in the back end (snake_case). */
export type CalendarFixture = Record<string, unknown>;

export function useCalendarFixture() {
  return useQuery({
    queryKey: calendarFixtureKey,
    queryFn: () => http<CalendarFixture>('/dev/calendar-fixture'),
  });
}

export function useReplaceCalendarFixture() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (fixture: CalendarFixture) =>
      http<void>('/dev/calendar-fixture', { method: 'PUT', body: JSON.stringify(fixture) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: calendarFixtureKey }),
  });
}

export function useResetCalendarFixture() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => http<void>('/dev/calendar-fixture/reset', { method: 'POST' }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: calendarFixtureKey }),
  });
}
