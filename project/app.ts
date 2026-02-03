type User = {
  name: string;
  age: number;
};

export function formatUser(user: User): string {
  return `${user.name} (${user.age})`;
}

export function isAdult(age: number): boolean {
  return age >= 18;
}
