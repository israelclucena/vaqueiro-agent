import { Component, input, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'ng-m3-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<div class="ng-m3-card" [class.ng-m3-card--elevated]="elevated()"><ng-content /></div>`,
  styleUrl: './ng-m3-card.component.scss',
})
export class NgM3CardComponent {
  readonly elevated = input(false);
}
