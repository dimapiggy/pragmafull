export function numberFormat(num?: number | null) {
  if (!num || typeof num !== 'number') {
    return 0;
  }

  return new Intl.NumberFormat('ru-RU').format(num);
}

// удаляет фильтры null и undefined
export function prepareFilters(stateFilters: Record<string, unknown>) {
  const filters = { ...stateFilters };

  Object.entries(stateFilters).forEach(([key, value]) => {
    if (value === null || value === undefined) {
      // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
      delete filters[key];
    }
  });

  return filters;
}

// правильное склонение слов с числительными
export function declOfNum(number: number, words: [string, string, string]) {
  return words[(number % 100 > 4 && number % 100 < 20) ? 2 : [2, 0, 1, 1, 1, 2][(number % 10 < 5) ? number % 10 : 5]];
}

// загрузка файла из blob
export function downloadBlob(blob: Blob, filename = 'untitled') {
  const objectUrl = URL.createObjectURL(blob);

  const link = document.createElement('a');

  link.setAttribute('href', objectUrl);
  link.setAttribute('download', filename);
  link.style.display = 'none';

  document.body.appendChild(link);

  link.click();

  document.body.removeChild(link);
  URL.revokeObjectURL(objectUrl);
}

// сокращенная функция для подъема страницы наверх
export function scrollTop(behavior: 'instant' | 'smooth' = 'instant') {
  window.scrollTo({ top: 0, left: 0, behavior });
}

// горизонтальный скролл элементов колесиком мышки
export function horizontalWheelScrollHandler(event: WheelEvent, el: HTMLElement | null) {
  if (el && el.scrollWidth > el.clientWidth) {
    event.preventDefault();

    if (event.deltaY > 0) el.scrollLeft += 30;
    else el.scrollLeft -= 30;
  }
}

// красивый вывод телефонов
export function phoneFormatted(phone?: string | null) {
  if (!phone) return '—';

  const _phone = !phone.startsWith('+') ? `+${phone}` : phone;
  return `${_phone.slice(0, 2)} (${_phone.slice(2, 5)}) ${_phone.slice(5, 8)}-${_phone.slice(8, 10)}-${_phone.slice(10, 12)}`;
}

// обработчик кнопок "Назад" в системе
export async function backBtnHandler(route_name: string, to: string) {
  const route = useRoute();
  const router = useRouter();

  router.go(-1);
  await nextTick();

  if (route.name === route_name) {
    await router.push(to);
  }
}

// клонирование простых объектов
export function cloneObject<T>(obj: unknown): T {
  return JSON.parse(JSON.stringify(obj));
}

// сравнение простых объектов
export function compareObject(obj1: unknown, obj2: unknown) {
  return JSON.stringify(obj1) === JSON.stringify(obj2);
}
