export interface dattType {
  main: {
    title: [string, string];
    description: string;
    features: {
      name: string;
      lekhan_sahayika: { title: string; lekh_md: string };
      phonetic_table: { title: string; lekh_md: string };
      brahmic_support: { title: string; lekh_md: string };
      parivartak: { title: string; lekh_md: string };
    };
  };
}
