import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedDataService {
  private currentAlbumNameSubject = new BehaviorSubject<string>('');
  public currentAlbumName$ = this.currentAlbumNameSubject.asObservable();

  constructor() { }

  setCurrentAlbumName(albumName: string) {
    this.currentAlbumNameSubject.next(albumName);
  }
}
