import read from 'datalib/src/import/read';
import dlstats from 'datalib/src/stats';
export default function data2schema(data) {
    const readData = read(data);
    const summary = dlstats.summary(readData);
    const keyedSummary = {};
    summary.forEach((column) => {
        const field = column.field;
        delete column.field;
        keyedSummary[field] = column;
    });
    return {
        stats: keyedSummary,
        size: data.length,
    };
}
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF0YTJzY2hlbWEuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvZGF0YTJzY2hlbWEudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxJQUFJLE1BQU0seUJBQXlCLENBQUM7QUFDM0MsT0FBTyxPQUFPLE1BQU0sbUJBQW1CLENBQUM7QUFPeEMsTUFBTSxDQUFDLE9BQU8sVUFBVSxXQUFXLENBQUMsSUFBVztJQUM3QyxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDNUIsTUFBTSxPQUFPLEdBQUcsT0FBTyxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUUxQyxNQUFNLFlBQVksR0FBRyxFQUFFLENBQUM7SUFDeEIsT0FBTyxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQVcsRUFBRSxFQUFFO1FBQzlCLE1BQU0sS0FBSyxHQUFHLE1BQU0sQ0FBQyxLQUFLLENBQUM7UUFDM0IsT0FBTyxNQUFNLENBQUMsS0FBSyxDQUFDO1FBQ3BCLFlBQVksQ0FBQyxLQUFLLENBQUMsR0FBRyxNQUFNLENBQUM7SUFDL0IsQ0FBQyxDQUFDLENBQUM7SUFFSCxPQUFPO1FBQ0wsS0FBSyxFQUFFLFlBQVk7UUFDbkIsSUFBSSxFQUFFLElBQUksQ0FBQyxNQUFNO0tBQ2xCLENBQUM7QUFDSixDQUFDIn0=