export default function json2constraints(json) {
    const type = json[0].type;
    json.forEach(constraint => {
        if (constraint.type !== type) {
            throw new Error(`constraints not all of type ${type}`);
        }
    });
    let definitions = '';
    let weights;
    let assigns;
    if (type === 'soft') {
        weights = '';
        assigns = '';
    }
    for (const constraint of json) {
        const def = `% @constraint ${constraint.description}
${constraint.asp}`;
        definitions += def;
        definitions += '\n\n';
        if (type === 'soft') {
            const weight = `#const ${constraint.name}_weight = ${constraint.weight}.`;
            weights += weight;
            weights += '\n';
            const assign = `soft_weight(${constraint.name}, ${constraint.name}_weight).`;
            assigns += assign;
            assigns += '\n';
        }
    }
    if (type === 'hard') {
        return { definitions };
    }
    else {
        return {
            definitions,
            weights,
            assigns,
        };
    }
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianNvbjJjb25zdHJhaW50cy5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9qc29uMmNvbnN0cmFpbnRzLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQVFBLE1BQU0sQ0FBQyxPQUFPLFVBQVUsZ0JBQWdCLENBQUMsSUFBa0I7SUFDekQsTUFBTSxJQUFJLEdBQUcsSUFBSSxDQUFDLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQztJQUMxQixJQUFJLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxFQUFFO1FBQ3hCLElBQUksVUFBVSxDQUFDLElBQUksS0FBSyxJQUFJLEVBQUU7WUFDNUIsTUFBTSxJQUFJLEtBQUssQ0FBQywrQkFBK0IsSUFBSSxFQUFFLENBQUMsQ0FBQztTQUN4RDtJQUNILENBQUMsQ0FBQyxDQUFDO0lBRUgsSUFBSSxXQUFXLEdBQUcsRUFBRSxDQUFDO0lBQ3JCLElBQUksT0FBTyxDQUFDO0lBQ1osSUFBSSxPQUFPLENBQUM7SUFDWixJQUFJLElBQUksS0FBSyxNQUFNLEVBQUU7UUFDbkIsT0FBTyxHQUFHLEVBQUUsQ0FBQztRQUNiLE9BQU8sR0FBRyxFQUFFLENBQUM7S0FDZDtJQUVELEtBQUssTUFBTSxVQUFVLElBQUksSUFBSSxFQUFFO1FBQzdCLE1BQU0sR0FBRyxHQUFHLGlCQUFpQixVQUFVLENBQUMsV0FBVztFQUNyRCxVQUFVLENBQUMsR0FBRyxFQUFFLENBQUM7UUFDZixXQUFXLElBQUksR0FBRyxDQUFDO1FBQ25CLFdBQVcsSUFBSSxNQUFNLENBQUM7UUFFdEIsSUFBSSxJQUFJLEtBQUssTUFBTSxFQUFFO1lBQ25CLE1BQU0sTUFBTSxHQUFHLFVBQVUsVUFBVSxDQUFDLElBQUksYUFBYSxVQUFVLENBQUMsTUFBTSxHQUFHLENBQUM7WUFDMUUsT0FBTyxJQUFJLE1BQU0sQ0FBQztZQUNsQixPQUFPLElBQUksSUFBSSxDQUFDO1lBRWhCLE1BQU0sTUFBTSxHQUFHLGVBQWUsVUFBVSxDQUFDLElBQUksS0FBSyxVQUFVLENBQUMsSUFBSSxXQUFXLENBQUM7WUFDN0UsT0FBTyxJQUFJLE1BQU0sQ0FBQztZQUNsQixPQUFPLElBQUksSUFBSSxDQUFDO1NBQ2pCO0tBQ0Y7SUFFRCxJQUFJLElBQUksS0FBSyxNQUFNLEVBQUU7UUFDbkIsT0FBTyxFQUFFLFdBQVcsRUFBRSxDQUFDO0tBQ3hCO1NBQU07UUFDTCxPQUFPO1lBQ0wsV0FBVztZQUNYLE9BQU87WUFDUCxPQUFPO1NBQ1IsQ0FBQztLQUNIO0FBQ0gsQ0FBQyJ9