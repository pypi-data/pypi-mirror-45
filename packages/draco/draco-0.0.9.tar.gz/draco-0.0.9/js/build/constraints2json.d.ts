interface Doc {
    description: string;
}
interface Asp {
    type: string;
    name: string;
    asp: string;
}
export interface Constraint extends Doc, Asp {
    weight?: number;
}
export default function constraints2json(constraintsAsp: string, weightsAsp?: string): Constraint[];
export {};
