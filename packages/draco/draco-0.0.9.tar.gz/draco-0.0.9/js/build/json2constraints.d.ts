import { Constraint } from './constraints2json';
export interface ConstraintAsp {
    definitions: string;
    weights?: string;
    assigns?: string;
}
export default function json2constraints(json: Constraint[]): ConstraintAsp;
