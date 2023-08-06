export default function schema2asp(schema) {
    if (!schema) {
        throw Error('No data has been prepared');
    }
    const stats = schema.stats;
    const decl = [`num_rows(${schema.size}).\n`];
    Object.keys(stats).forEach((field, i) => {
        const fieldName = `\"${field}\"`;
        const fieldStats = stats[field];
        const fieldType = `fieldtype(${fieldName},${fieldStats.type}).`;
        const cardinality = `cardinality(${fieldName}, ${fieldStats.distinct}).`;
        decl.push(`${fieldType}\n${cardinality}`);
    });
    return decl;
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic2NoZW1hMmFzcC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NyYy9zY2hlbWEyYXNwLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUVBLE1BQU0sQ0FBQyxPQUFPLFVBQVUsVUFBVSxDQUFDLE1BQWM7SUFDL0MsSUFBSSxDQUFDLE1BQU0sRUFBRTtRQUNYLE1BQU0sS0FBSyxDQUFDLDJCQUEyQixDQUFDLENBQUM7S0FDMUM7SUFFRCxNQUFNLEtBQUssR0FBRyxNQUFNLENBQUMsS0FBSyxDQUFDO0lBQzNCLE1BQU0sSUFBSSxHQUFHLENBQUMsWUFBWSxNQUFNLENBQUMsSUFBSSxNQUFNLENBQUMsQ0FBQztJQUU3QyxNQUFNLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDLEVBQUUsRUFBRTtRQUN0QyxNQUFNLFNBQVMsR0FBRyxLQUFLLEtBQUssSUFBSSxDQUFDO1FBQ2pDLE1BQU0sVUFBVSxHQUFHLEtBQUssQ0FBQyxLQUFLLENBQUMsQ0FBQztRQUNoQyxNQUFNLFNBQVMsR0FBRyxhQUFhLFNBQVMsSUFBSSxVQUFVLENBQUMsSUFBSSxJQUFJLENBQUM7UUFDaEUsTUFBTSxXQUFXLEdBQUcsZUFBZSxTQUFTLEtBQUssVUFBVSxDQUFDLFFBQVEsSUFBSSxDQUFDO1FBRXpFLElBQUksQ0FBQyxJQUFJLENBQUMsR0FBRyxTQUFTLEtBQUssV0FBVyxFQUFFLENBQUMsQ0FBQztJQUM1QyxDQUFDLENBQUMsQ0FBQztJQUVILE9BQU8sSUFBSSxDQUFDO0FBQ2QsQ0FBQyJ9