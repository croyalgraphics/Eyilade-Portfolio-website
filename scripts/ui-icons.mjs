// Local interface glyphs made from basic SVG geometry; brand marks remain supplied assets.
const paths={
 copy:'<rect x="8" y="8" width="12" height="12" rx="3"/><path d="M15 5V4a1 1 0 0 0-1-1H5a2 2 0 0 0-2 2v9a1 1 0 0 0 1 1h1"/>',
 plus:'<path d="M12 5v14M5 12h14"/>',
 check:'<path d="m5 12 4 4L19 6"/>',
 download:'<path d="M12 3v12m-5-5 5 5 5-5M4 16v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/>',
 left:'<path d="m14 6-6 6 6 6"/>',right:'<path d="m10 6 6 6-6 6"/>',
 sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
 moon:'<path d="M20.5 13.2A8.7 8.7 0 0 1 10.8 3.5a8.7 8.7 0 1 0 9.7 9.7Z"/>',
 motion:'<path d="M3 7h4M1 12h4m-2 5h4"/><circle cx="15" cy="12" r="8"/><path class="motion-pause-lines" d="M13 9v6m4-6v6"/><path class="motion-play-triangle" d="m13 8 5 4-5 4Z"/>'
};
export function icon(name,cls=''){return `<svg class="ui-icon ${cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name]||''}</svg>`;}
