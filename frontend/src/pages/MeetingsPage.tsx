import { Alert, Button, Group, Stack, Text, Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconRefresh } from '@tabler/icons-react';

import { useMeetings, useSyncMeetings } from '../api/meetings';
import { CalendarConnectionsCard } from '../components/CalendarConnectionsCard';
import { MeetingRow } from '../components/MeetingRow';

export function MeetingsPage() {
  const meetings = useMeetings();
  const sync = useSyncMeetings();

  const syncMeetings = () =>
    sync.mutate(undefined, {
      onSuccess: () => notifications.show({ message: 'Meetings synced' }),
      onError: (error) => notifications.show({ color: 'red', title: 'Sync failed', message: error.message }),
    });

  return (
    <Stack maw={880} mx="auto">
      <Group justify="space-between">
        <div>
          <Title order={2}>Meetings</Title>
          <Text c="dimmed">Synced from connected calendars</Text>
        </div>
        <Button leftSection={<IconRefresh size={16} />} onClick={syncMeetings} loading={sync.isPending}>
          Sync meetings
        </Button>
      </Group>

      <CalendarConnectionsCard />

      <Title order={4} mt="md">
        Upcoming meetings
      </Title>
      {meetings.error && <Alert color="red">{meetings.error.message}</Alert>}
      {meetings.data?.length === 0 && <Text c="dimmed">No meetings yet. Sync to pull them from calendars.</Text>}
      <Stack gap="sm">
        {meetings.data?.map((meeting) => <MeetingRow key={meeting.id} meeting={meeting} />)}
      </Stack>
    </Stack>
  );
}
