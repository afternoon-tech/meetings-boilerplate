import { Alert, Button, Drawer, Group, JsonInput, Stack, Text } from '@mantine/core';
import { useEffect, useState } from 'react';

import { useCalendarFixture, useReplaceCalendarFixture, useResetCalendarFixture } from '../api/calendarFixture';

interface Props {
  opened: boolean;
  onClose: () => void;
}

/** Dev tool: edit what the stubbed Google/Microsoft calendars return, to simulate changes made remotely. */
export function CalendarFixtureDrawer({ opened, onClose }: Props) {
  const fixture = useCalendarFixture();
  const replace = useReplaceCalendarFixture();
  const reset = useResetCalendarFixture();
  const [draft, setDraft] = useState('');

  useEffect(() => {
    if (fixture.data) {
      setDraft(JSON.stringify(fixture.data, null, 2));
    }
  }, [fixture.data]);

  const save = () => replace.mutate(JSON.parse(draft));

  return (
    <Drawer opened={opened} onClose={onClose} position="right" size="xl" title="Calendar fixture">
      <Stack>
        <Text size="sm" c="dimmed">
          What each connected calendar returns on the next sync, keyed by calendar connection id. Changes are held in
          memory and lost when the API restarts.
        </Text>
        {replace.error && <Alert color="red">{replace.error.message}</Alert>}
        <JsonInput value={draft} onChange={setDraft} autosize minRows={20} maxRows={40} validationError="Invalid JSON" />
        <Group justify="flex-end">
          <Button variant="default" onClick={() => reset.mutate()} loading={reset.isPending}>
            Reset to default
          </Button>
          <Button onClick={save} loading={replace.isPending}>
            Save
          </Button>
        </Group>
      </Stack>
    </Drawer>
  );
}
