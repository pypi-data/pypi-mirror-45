const HOLE = '?';
export default function cql2asp(spec) {
    const mark = subst_if_hole(spec.mark);
    const facts = [];
    if (mark) {
        facts.push(`mark(${spec.mark}).`);
    }
    if ('data' in spec && 'url' in spec.data) {
        facts.push(`data("${spec.data.url}").`);
    }
    for (let i = 0; i < spec.encodings.length; i++) {
        const enc = spec.encodings[i];
        const eid = `e${i}`;
        facts.push(`encoding(${eid}).`);
        let encFieldType = null;
        let encZero = null;
        let encBinned = null;
        for (const field of Object.keys(enc)) {
            const fieldContent = subst_if_hole(enc[field]);
            if (!fieldContent) {
                continue;
            }
            if (!remove_if_star(fieldContent)) {
                continue;
            }
            if (field === 'type') {
                encFieldType = fieldContent;
            }
            if (field === 'bin') {
                encBinned = fieldContent;
            }
            if (field === 'scale') {
                // translate two boolean fields
                if ('zero' in fieldContent) {
                    encZero = fieldContent.zero;
                    if (fieldContent.zero) {
                        facts.push(`zero(${eid}).`);
                    }
                    else {
                        facts.push(`:- zero(${eid}).`);
                    }
                }
                if ('log' in fieldContent) {
                    if (fieldContent.log) {
                        facts.push(`log(${eid}).`);
                    }
                    else {
                        facts.push(`:-log(${eid}).`);
                    }
                }
            }
            else if (field === 'bin') {
                if (fieldContent.maxbins) {
                    facts.push(`${field}(${eid},${fieldContent.maxbins}).`);
                }
                else if (fieldContent) {
                    facts.push(`:- not bin(${eid},_).`);
                }
                else {
                    facts.push(`:- bin(${eid},_).`);
                }
            }
            else if (field === 'field') {
                // fields can have spaces and start with capital letters
                facts.push(`${field}(${eid},"${fieldContent}").`);
            }
            else {
                // translate normal fields
                if (field !== 'bin') {
                    facts.push(`${field}(${eid},${fieldContent}).`);
                }
            }
        }
        if (encFieldType === 'quantitative' && encZero === null && encBinned === null) {
            facts.push(`zero(${eid}).`);
        }
    }
    return facts;
}
function subst_if_hole(v) {
    return v !== HOLE ? v : null;
}
function remove_if_star(v) {
    return v !== '*' ? v : null;
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY3FsMmFzcC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9jcWwyYXNwLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBLE1BQU0sSUFBSSxHQUFHLEdBQUcsQ0FBQztBQUVqQixNQUFNLENBQUMsT0FBTyxVQUFVLE9BQU8sQ0FBQyxJQUFTO0lBQ3ZDLE1BQU0sSUFBSSxHQUFHLGFBQWEsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7SUFFdEMsTUFBTSxLQUFLLEdBQUcsRUFBRSxDQUFDO0lBRWpCLElBQUksSUFBSSxFQUFFO1FBQ1IsS0FBSyxDQUFDLElBQUksQ0FBQyxRQUFRLElBQUksQ0FBQyxJQUFJLElBQUksQ0FBQyxDQUFDO0tBQ25DO0lBRUQsSUFBSSxNQUFNLElBQUksSUFBSSxJQUFJLEtBQUssSUFBSSxJQUFJLENBQUMsSUFBSSxFQUFFO1FBQ3hDLEtBQUssQ0FBQyxJQUFJLENBQUMsU0FBUyxJQUFJLENBQUMsSUFBSSxDQUFDLEdBQUcsS0FBSyxDQUFDLENBQUM7S0FDekM7SUFFRCxLQUFLLElBQUksQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQyxNQUFNLEVBQUUsQ0FBQyxFQUFFLEVBQUU7UUFDOUMsTUFBTSxHQUFHLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUM5QixNQUFNLEdBQUcsR0FBRyxJQUFJLENBQUMsRUFBRSxDQUFDO1FBQ3BCLEtBQUssQ0FBQyxJQUFJLENBQUMsWUFBWSxHQUFHLElBQUksQ0FBQyxDQUFDO1FBRWhDLElBQUksWUFBWSxHQUFHLElBQUksQ0FBQztRQUN4QixJQUFJLE9BQU8sR0FBRyxJQUFJLENBQUM7UUFDbkIsSUFBSSxTQUFTLEdBQUcsSUFBSSxDQUFDO1FBRXJCLEtBQUssTUFBTSxLQUFLLElBQUksTUFBTSxDQUFDLElBQUksQ0FBQyxHQUFHLENBQUMsRUFBRTtZQUNwQyxNQUFNLFlBQVksR0FBRyxh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