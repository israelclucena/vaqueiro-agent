import { Component, signal, computed } from '@angular/core';
import { NgM3ButtonComponent } from '../lib/button/ng-m3-button.component';
import { NgM3CardComponent } from '../lib/card/ng-m3-card.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NgM3ButtonComponent, NgM3CardComponent],
  template: `
    <ng-m3-card [elevated]="true">
      @if (count() > 0) {
        <p>Clicked {{ count() }} times ({{ parity() }}).</p>
      } @else {
        <p>Not clicked yet.</p>
      }
      <ng-m3-button variant="filled" (pressed)="inc()">Increment</ng-m3-button>
    </ng-m3-card>
  `,
})
export class AppComponent {
  protected readonly count = signal(0);
  protected readonly parity = computed(() => (this.count() % 2 === 0 ? 'even' : 'odd'));
  protected inc(): void {
    this.count.update((c) => c + 1);
  }
}
