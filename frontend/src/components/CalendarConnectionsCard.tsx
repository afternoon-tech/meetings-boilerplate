import { Badge, Card, Group, Stack, Text, Title } from '@mantine/core';
import dayjs from 'dayjs';

import type { CalendarProvider } from '../api/meetings';
import { useCalendarConnections } from '../api/meetings';

const providerLabels: Record<CalendarProvider, string> = {
  GOOGLE: 'Google',
  MICROSOFT: 'Microsoft',
};

export function CalendarConnectionsCard() {
  const { data: connections = [], isLoading } = useCalendarConnections();

  return (
    <Card withBorder padding="lg">
      <Title order={4} mb="sm">
        Connected calendars
      </Title>
      {isLoading && <Text c="dimmed">Loading…</Text>}
      <Stack gap="xs">
        {connections.map((connection) => (
          <Group key={connection.id} justify="space-between">
            <Group gap="sm">
              <Text fw={500}>{connection.advisor.name}</Text>
              <Badge variant="light">{providerLabels[connection.provider]}</Badge>
            </Group>
            <Text size="sm" c="dimmed">
              {connection.lastSyncedAt
                ? `Last synced ${dayjs(connection.lastSyncedAt).format('D MMM, HH:mm')}`
                : 'Never synced'}
            </Text>
          </Group>
        ))}
      </Stack>
    </Card>
  );
}
