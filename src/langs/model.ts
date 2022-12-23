export interface dattType {
  main: {
    title: [string, string];
    description: string;
    features: {
      name: string;
      lekhan_sahayika: { title: string; lekh: string };
      phonetic_table: { title: string; lekh: string };
      brahmic_support: { title: string; lekh: string };
      parivartak: { title: string; lekh: string };
    };
  };
}
