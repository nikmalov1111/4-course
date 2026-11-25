import * as migration_20261124_123505_initial from './20261124_123505_initial';

export const migrations = [
  {
    up: migration_20261124_123505_initial.up,
    down: migration_20261124_123505_initial.down,
    name: '20261124_123505_initial'
  },
];
