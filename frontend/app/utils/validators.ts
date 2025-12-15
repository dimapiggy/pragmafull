const specialSymbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '"', ':', ';', '"', '\'', '<', '>', ',', '.', '?', '/'];

export function isEmail(value: string | null) {
  return value?.trim().toLowerCase().match(/^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$/);
}

export function isPhone(value: string | null) {
  const onlyNumbers = value?.replace(/\D/g, '') || '';

  return value?.trim().match(/^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$/) && onlyNumbers.length === 11;
}

export function minLength(value: string | number, length: number) {
  return value.toString().length >= length;
}

export function containsLetter(value: string) {
  return /\D/g.test(value);
}

export function containsUpperCase(value: string) {
  return value !== value.toLowerCase();
}

export function containsLowerCase(value: string) {
  return value !== value.toUpperCase();
}

export function containsNumber(value: string) {
  return /\d/g.test(value);
}

export function containsSpecialSymbol(value: string) {
  return specialSymbols.some(item => value.includes(item));
}

export function isValidPassword(value: string) {
  return minLength(value, 9) && containsLetter(value) && containsNumber(value);
}
