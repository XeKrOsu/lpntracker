class Storage {
    static saveEmployees(employees) {
        localStorage.setItem('employees', JSON.stringify(employees));
    }

    static loadEmployees() {
        const storedEmployees = localStorage.getItem('employees');
        if (storedEmployees) {
            const employees = JSON.parse(storedEmployees);
            employees.forEach(emp => {
                emp.startDate = new Date(emp.startDate);
                emp.lastMissionDate = emp.lastMissionDate === 'N/A' ? 'N/A' : new Date(emp.lastMissionDate);
                emp.missions.forEach(mission => {
                    mission.date = new Date(mission.date);
                });
            });
            return employees;
        }
        return [];
    }
}
