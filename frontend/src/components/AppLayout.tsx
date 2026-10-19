import { AppShell, Button, Group, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconFlask } from '@tabler/icons-react';
import { Outlet } from 'react-router';

import { CalendarFixtureDrawer } from './CalendarFixtureDrawer';

export function AppLayout() {
  const [fixtureOpened, fixture] = useDisclosure(false);

  return (
    <AppShell header={{ height: 56 }} padding="lg">
      <AppShell.Header>
        <Group h="100%" px="lg" justify="space-between">
          <Text fw={700}>Harbour Wealth</Text>
          <Button variant="subtle" size="xs" leftSection={<IconFlask size={14} />} onClick={fixture.open}>
            Calendar fixture
          </Button>
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
      <CalendarFixtureDrawer opened={fixtureOpened} onClose={fixture.close} />
    </AppShell>
  );
}
