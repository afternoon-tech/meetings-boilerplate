import { Card, Group, Stack, Text } from '@mantine/core';
import dayjs from 'dayjs';

import type { Meeting } from '../api/meetings';

export function MeetingRow({ meeting }: { meeting: Meeting }) {
  const startsAt = dayjs(meeting.startsAt);

  return (
    <Card withBorder padding="md">
      <Group wrap="nowrap" align="flex-start">
        <Stack gap={0} align="center" w={48}>
          <Text size="xl" fw={700} lh={1}>
            {startsAt.format('D')}
          </Text>
          <Text size="xs" tt="uppercase" c="dimmed">
            {startsAt.format('MMM')}
          </Text>
        </Stack>
        <Stack gap={2}>
          <Text fw={600}>{meeting.title}</Text>
          <Text size="sm" c="dimmed">
            {startsAt.format('HH:mm')}–{dayjs(meeting.endsAt).format('HH:mm')}
          </Text>
        </Stack>
      </Group>
    </Card>
  );
}
