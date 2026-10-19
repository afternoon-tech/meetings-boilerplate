import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

import type { CalendarConnection, Meeting } from '../api/meetings';
import { MeetingsPage } from './MeetingsPage';

const meetings: Meeting[] = [
  { id: 'm1', title: 'Annual financial review', startsAt: '2026-10-21T10:00:00Z', endsAt: '2026-10-21T11:00:00Z' },
];

const connections: CalendarConnection[] = [
  {
    id: 'c1',
    provider: 'GOOGLE',
    accountEmail: 'alice@harbourwealth.co.uk',
    advisor: { id: 'a1', name: 'Alice Carter', email: 'alice@harbourwealth.co.uk' },
    lastSyncedAt: null,
  },
];

function stubApi(responses: Record<string, unknown>) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (path: string) => new Response(JSON.stringify(responses[path]), { status: 200 })),
  );
}

function renderPage() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <MantineProvider>
      <QueryClientProvider client={queryClient}>
        <MeetingsPage />
      </QueryClientProvider>
    </MantineProvider>,
  );
}

afterEach(() => vi.unstubAllGlobals());

test('lists meetings and connected calendars', async () => {
  stubApi({ '/api/meetings': meetings, '/api/calendar-connections': connections });

  renderPage();

  expect(await screen.findByText('Annual financial review')).toBeInTheDocument();
  expect(await screen.findByText('Alice Carter')).toBeInTheDocument();
});
