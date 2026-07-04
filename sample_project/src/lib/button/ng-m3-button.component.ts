import { Component, input, output, ChangeDetectionStrategy } from '@angular/core';

export type NgM3ButtonVariant = 'filled' | 'outlined' | 'text';

@Component({
  selector: 'ng-m3-button',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './ng-m3-button.component.html',
  styleUrl: './ng-m3-button.component.scss',
})
export class NgM3ButtonComponent {
  readonly variant = input<NgM3ButtonVariant>('filled');
  readonly disabled = input(false);
  readonly pressed = output<void>();

  protected onClick(): void {
    if (!this.disabled()) {
      this.pressed.emit();
    }
  }
}
