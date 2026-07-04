import type { Meta, StoryObj } from '@storybook/angular';
import { NgM3ButtonComponent } from './ng-m3-button.component';

const meta: Meta<NgM3ButtonComponent> = {
  title: 'Components/Button',
  component: NgM3ButtonComponent,
  args: { variant: 'filled', disabled: false },
};
export default meta;

type Story = StoryObj<NgM3ButtonComponent>;
export const Filled: Story = { args: { variant: 'filled' } };
export const Outlined: Story = { args: { variant: 'outlined' } };
export const Text: Story = { args: { variant: 'text' } };
