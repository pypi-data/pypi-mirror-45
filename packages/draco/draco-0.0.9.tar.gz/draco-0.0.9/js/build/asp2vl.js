const REGEX = /(\w+)\(([\w\.\/]+)(,([\w\.]+))?\)/;
/**
 * Convert from ASP to Vega-Lite.
 */
export default function asp2vl(facts) {
    let mark = '';
    let url = 'data/cars.json'; // default dataset
    const encodings = {};
    for (const value of facts) {
        // TODO: Better handle quoted fields. We currently simply remove all ".
        const cleanedValue = value.replace(/\"/g, '');
        const negSymbol = value.trim().startsWith(':-'); // TODO: remove this
        const [_, predicate, first, __, second] = REGEX.exec(cleanedValue);
        if (predicate === 'mark') {
            mark = first;
        }
        else if (predicate === 'data') {
            url = first;
        }
        else if (predicate !== 'soft') {
            if (!encodings[first]) {
                encodings[first] = {};
            }
            // if it contains the neg symbol, and the field is a boolean field, its value would be false
            // e.g., for the case ":- zero(e3)"
            encodings[first][predicate] = second || !negSymbol;
        }
    }
    const encoding = {};
    for (const e of Object.keys(encodings)) {
        const enc = encodings[e];
        // if quantitative encoding and zero is not set, set zero to false
        if (enc.type === 'quantitative' && enc.zero === undefined && enc.bin === undefined) {
            enc.zero = false;
        }
        const scale = {
            ...(enc.log ? { type: 'log' } : {}),
            ...(enc.zero === undefined ? {} : enc.zero ? { zero: true } : { zero: false }),
        };
        encoding[enc.channel] = {
            type: enc.type,
            ...(enc.aggregate ? { aggregate: enc.aggregate } : {}),
            ...(enc.field ? { field: enc.field } : {}),
            ...(enc.stack ? { stack: enc.stack } : {}),
            ...(enc.bin !== undefined ? (+enc.bin === 10 ? { bin: true } : { bin: { maxbins: +enc.bin } }) : {}),
            ...(Object.keys(scale).length ? { scale } : {}),
        };
    }
    return {
        $schema: 'https://vega.github.io/schema/vega-lite/v3.json',
        data: { url: `${url}` },
        mark,
        encoding,
    };
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYXNwMnZsLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4vc3JjL2FzcDJ2bC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFFQSxNQUFNLEtBQUssR0FBRyxtQ0FBbUMsQ0FBQztBQUVsRDs7R0FFRztBQUNILE1BQU0sQ0FBQyxPQUFPLFVBQVUsTUFBTSxDQUFDLEtBQWU7SUFDNUMsSUFBSSxJQUFJLEdBQUcsRUFBRSxDQUFDO0lBQ2QsSUFBSSxHQUFHLEdBQUcsZ0JBQWdCLENBQUMsQ0FBQyxrQkFBa0I7SUFDOUMsTUFBTSxTQUFTLEdBQTJCLEVBQUUsQ0FBQztJQUU3QyxLQUFLLE1BQU0sS0FBSyxJQUFJLEtBQUssRUFBRTtRQUN6Qix1RUFBdUU7UUFDdkUsTUFBTSxZQUFZLEdBQUcsS0FBSyxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsRUFBRSxDQUFDLENBQUM7UUFDOUMsTUFBTSxTQUFTLEdBQUcsS0FBSyxDQUFDLElBQUksRUFBRSxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLG9CQUFvQjtRQUNyRSxNQUFNLENBQUMsQ0FBQyxFQUFFLFNBQVMsRUFBRSxLQUFLLEVBQUUsRUFBRSxFQUFFLE1BQU0sQ0FBQyxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFRLENBQUM7UUFFMUUsSUFBSSxTQUFTLEtBQUssTUFBTSxFQUFFO1lBQ3hCLElBQUksR0FBRyxLQUFLLENBQUM7U0FDZDthQUFNLElBQUksU0FBUyxLQUFLLE1BQU0sRUFBRTtZQUMvQixHQUFHLEdBQUcsS0FBSyxDQUFDO1NBQ2I7YUFBTSxJQUFJLFNBQVMsS0FBSyxNQUFNLEVBQUU7WUFDL0IsSUFBSSxDQUFDLFNBQVMsQ0FBQyxLQUFLLENBQUMsRUFBRTtnQkFDckIsU0FBUyxDQUFDLEtBQUssQ0FBQyxHQUFHLEVBQUUsQ0FBQzthQUN2QjtZQUNELDRGQUE0RjtZQUM1RixtQ0FBbUM7WUFDbkMsU0FBUyxDQUFDLEtBQUssQ0FBQyxDQUFDLFNBQVMs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